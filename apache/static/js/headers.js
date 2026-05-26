function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);

    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }

    return undefined;
}

export function getHeaders(getCsrf) {
    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    if (getCsrf) {
        // Primero intenta obtener de sessionStorage (después del login)
        let token = sessionStorage.getItem('csrf_token');
        // Si no está en sessionStorage, intenta desde cookies
        if (!token) {
            token = getCookie('csrf_token');
        }
        if (token) {
            headers.append("X-CSRFToken", token);
        }
    }
    return headers;
}