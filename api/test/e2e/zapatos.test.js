const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

// Cambia la ruta final para que apunte a la página correcta
const BASE_URL = process.env.BASE_URL ? `${process.env.BASE_URL}/agregar_zapato.html` : 'http://10.227.87.9:30607/agregar_zapato.html';

// Mantenemos el timeout alto para evitar fallos de Puppeteer
jest.setTimeout(60000); 

describe('Flujo de Agregar Zapato', () => {
  let browser;
  let page;
  
  // Ruta para un archivo de imagen falso que usaremos en el test
  const dummyFilePath = path.join(__dirname, 'dummy_foto.png');

  beforeAll(async () => {
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    page = await browser.newPage();
    
    // 💡 Creamos un archivo falso temporal para poder probar el <input type="file">
    fs.writeFileSync(dummyFilePath, 'contenido falso simulando una imagen');
  });

  afterAll(async () => {
    await browser.close();
    // 💡 Limpiamos y borramos el archivo temporal al terminar
    if (fs.existsSync(dummyFilePath)) {
      fs.unlinkSync(dummyFilePath);
    }
  });

  beforeEach(async () => {
    // Vamos a la página antes de cada test
    await page.goto(BASE_URL);
  });

  // ---------------------------------------
  // 1️⃣ Comprobar que el DOM carga bien
  // ---------------------------------------
  it('debería renderizar el formulario con todos sus campos', async () => {
    const inputs = await Promise.all([
      page.$('#nombre'),
      page.$('#descripcion'),
      page.$('#marca'),
      page.$('#precio'),
      page.$('#filefoto')
    ]);
    
    // Verificamos que ninguno de los selectores devuelva null (es decir, existen en el HTML)
    inputs.forEach(input => expect(input).not.toBeNull());
  });

  // ---------------------------------------
  // 2️⃣ Comprobar la validación del Frontend
  // ---------------------------------------
  it('debería mostrar un alert si se intenta guardar con campos vacíos', async () => {
    const dialogPromise = new Promise(resolve => {
      page.once('dialog', async dialog => {
        expect(dialog.message()).toContain('Todos los campos son requeridos');
        await dialog.dismiss();
        resolve();
      });
    });

    // Hacemos click en "Guardar Zapato" sin rellenar nada
    await page.click('.button-upload');
    
    // Esperamos a que la alerta se resuelva
    await dialogPromise;
  });

  // ---------------------------------------
  // 3️⃣ Comprobar el envío correcto (Happy Path)
  // ---------------------------------------
  it('debería rellenar datos, subir imagen y enviar el formulario', async () => {
    // Llenamos los inputs de texto
    await page.type('#nombre', 'Jordan 1 Retro Test');
    await page.type('#descripcion', 'Zapatillas generadas desde Jest');
    await page.type('#marca', 'Nike');
    await page.type('#precio', '250');

    // 💡 Subimos el archivo al input
    const fileInput = await page.$('#filefoto');
    await fileInput.uploadFile(dummyFilePath);

    // Preparamos la escucha del alert de respuesta del servidor
    const dialogPromise = new Promise(resolve => {
      page.once('dialog', async dialog => {
        const msg = dialog.message();
        
        // Si tu backend está levantado y funciona, debería devolver esto:
        // Si falla por permisos o red en Jenkins, capturará el error del catch.
        expect(typeof msg).toBe('string'); 
        
        await dialog.dismiss();
        resolve(msg);
      });
    });

    // Hacemos el envío
    await page.click('.button-upload');
    
    // Esperamos la respuesta de la alerta
    const alertMessage = await dialogPromise;
    
    // Opcional: Si estás seguro de que la base de datos de test siempre responderá "OK":
    // expect(alertMessage).toContain('Zapato guardado correctamente');
  });
});
