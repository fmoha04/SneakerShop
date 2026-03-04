const puppeteer = require('puppeteer');

// ⚠️ IMPORTANTE: Cambia 'editar_zapato.html' por el nombre real de tu archivo HTML
const BASE_URL = process.env.BASE_URL ? `${process.env.BASE_URL}/editar_zapato.html` : 'http://10.227.87.9:30607/editar_zapato.html';

jest.setTimeout(60000);

describe('Flujo de Editar Zapato', () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
  });

  afterAll(async () => {
    await browser.close();
  });

  beforeEach(async () => {
    page = await browser.newPage();
    // 💡 Activamos la intercepción de red. Esto nos permite simular las respuestas del backend
    await page.setRequestInterception(true);
  });

  afterEach(async () => {
    await page.close();
  });

  // ---------------------------------------
  // 1️⃣ Carga inicial de datos (GET)
  // ---------------------------------------
  it('debería obtener los datos del zapato y rellenar el formulario', async () => {
    // Interceptamos la petición GET y devolvemos un zapato simulado
    page.on('request', interceptedRequest => {
      if (interceptedRequest.url().includes('/api/zapatos/999') && interceptedRequest.method() === 'GET') {
        interceptedRequest.respond({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            id: 999,
            nombre: "Zapato Mock",
            descripcion: "Descripción simulada",
            marca: "Reebok",
            precio: 150,
            foto: "http://imagenfalsa.com/foto.png"
          })
        });
      } else {
        interceptedRequest.continue();
      }
    });

    // Navegamos a la página pasándole el ID 999
    await page.goto(`${BASE_URL}?id=999`, { waitUntil: 'networkidle0' });

    // Verificamos que el formulario se haya rellenado con los datos simulados
    const nombreValue = await page.$eval('#nombre', el => el.value);
    const marcaValue = await page.$eval('#marca', el => el.value);
    
    expect(nombreValue).toBe('Zapato Mock');
    expect(marcaValue).toBe('Reebok');
  });

  // ---------------------------------------
  // 2️⃣ Guardar cambios (PUT)
  // ---------------------------------------
  it('debería enviar los datos modificados y mostrar alert de éxito', async () => {
    page.on('request', interceptedRequest => {
      // Simulamos el GET inicial para que cargue la página
      if (interceptedRequest.method() === 'GET' && interceptedRequest.url().includes('/api/zapatos/')) {
        interceptedRequest.respond({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ id: 999, nombre: "Viejo", descripcion: "V", marca: "M", precio: 10, foto: "f.jpg" })
        });
      } 
      // Simulamos el PUT de actualización para que devuelva OK
      else if (interceptedRequest.method() === 'PUT' && interceptedRequest.url().includes('/api/zapatos/')) {
        interceptedRequest.respond({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ status: "OK" })
        });
      } else {
        interceptedRequest.continue();
      }
    });

    await page.goto(`${BASE_URL}?id=999`, { waitUntil: 'networkidle0' });

    // Modificamos un campo del formulario
    await page.click('#nombre', { clickCount: 3 }); // Selecciona todo el texto
    await page.type('#nombre', 'Zapato Actualizado');

    // Preparamos la promesa para capturar el alert
    const dialogPromise = new Promise(resolve => {
      page.once('dialog', async dialog => {
        expect(dialog.message()).toContain('zapato modificado correctamente');
        await dialog.dismiss();
        resolve();
      });
    });

    // Hacemos click en "Guardar Cambios"
    await page.click('.button-upload');
    
    // Esperamos a que salga el alert
    await dialogPromise;
  });

  // ---------------------------------------
  // 3️⃣ Manejo de error si el zapato no existe
  // ---------------------------------------
  it('debería mostrar un alert de error si falla la carga inicial', async () => {
    page.on('request', interceptedRequest => {
      if (interceptedRequest.url().includes('/api/zapatos/999') && interceptedRequest.method() === 'GET') {
        // Simulamos que el servidor devuelve un error 404 (no encontrado)
        interceptedRequest.respond({ status: 404 });
      } else {
        interceptedRequest.continue();
      }
    });

    const dialogPromise = new Promise(resolve => {
      page.once('dialog', async dialog => {
        expect(dialog.message()).toContain('Ha habido un error al recuperar los datos');
        await dialog.dismiss();
        resolve();
      });
    });

    // Al navegar, la página intentará hacer el fetch, fallará (porque le damos 404) y saltará el alert
    await page.goto(`${BASE_URL}?id=999`);
    await dialogPromise;
  });
});
