const puppeteer = require('puppeteer');

const BASE_URL = process.env.BASE_URL || 'http://10.227.87.9:30607';

// 💡 1. Aumentamos el timeout global de Jest para este archivo a 30 segundos.
// Esto sobrescribe el límite por defecto de 5 segundos.
jest.setTimeout(30000); 

describe('Flujos de Login y Sign Up', () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    page = await browser.newPage();
  });

  afterAll(async () => {
    await browser.close();
  });

  // ---------------------------------------
  // 1️⃣ Comprobar que las pestañas funcionan
  // ---------------------------------------
  it('debería cambiar entre pestañas Sign Up y Log In', async () => {
    await page.goto(BASE_URL);

    let signupVisible = await page.$eval('#signup', el => el.style.display !== 'none');
    let loginVisible = await page.$eval('#login', el => el.style.display !== 'none');
    expect(signupVisible).toBe(true);
    expect(loginVisible).toBe(false);

    await page.click('.tab a[href="#login"]');
    signupVisible = await page.$eval('#signup', el => el.style.display !== 'none');
    loginVisible = await page.$eval('#login', el => el.style.display !== 'none');
    expect(signupVisible).toBe(false);
    expect(loginVisible).toBe(true);
  });

  // ---------------------------------------
  // 4️⃣ Login con credenciales incorrectas
  // ---------------------------------------
  it('debería mostrar error con credenciales falsas en Login', async () => {
    await page.goto(BASE_URL);

    await page.click('.tab a[href="#login"]');

    await page.type('#username', 'usuario_falso');
    await page.type('#password', '12345');
    await page.click('#login .button-block');

    const errorTexto = await page.$eval('#login .error', el => el.textContent);
    expect(errorTexto).toContain('Usuario o contraseña incorrectos');
  });

  // ---------------------------------------
  // 5️⃣ Login con credenciales correctas (si existe)
  // ---------------------------------------
  it('debería loguear un usuario válido', async () => {
    await page.goto(BASE_URL);

    await page.click('.tab a[href="#login"]');

    const username = 'root';
    const password = '1234';

    await page.type('#username', username);
    await page.type('#password', password);

    // 💡 4. Evitar Race Conditions usando Promise.all
    // Siempre hay que esperar la navegación al MISMO TIEMPO que se hace el click.
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle0' }),
      page.click('#login .button-block')
    ]);

    expect(page.url()).toContain('zapatos.html');
  });
});
