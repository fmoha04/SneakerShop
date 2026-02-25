const puppeteer = require('puppeteer')

// Extract url from environment variables
const BASE_URL = process.env.BASE_URL || 'http://localhost:32769';

describe('Flujo de Login', () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch({
      headless: true, // Obligatorio para Jenkins
      args: ['--no-sandbox'] 
    });
    page = await browser.newPage();
  });

  it('debería mostrar error con credenciales falsas', async () => {
    await page.goto(BASE_URL);
    await page.type('#username_sign', 'usuario_falso');
    await page.type('#password_sign', '12345');
    await page.click('.button-block');
    
    const texto = await page.$eval('.error-msg', el => el.textContent);
    expect(texto).toContain('Credenciales inválidas');
  });

  afterAll(async () => {
    await browser.close();
  });
});
