export const API_BASE_URL =
  "http://127.0.0.1:8000";


function getToken() {
  return localStorage.getItem("mangocare_token");
}


function getAuthHeaders() {

  const token = getToken();

  return token
    ? {
        Authorization: `Bearer ${token}`
      }
    : {};
}


// ==================================================
// AUTHENTICATION
// ==================================================

export async function registerUser(userData) {

  const response = await fetch(
    `${API_BASE_URL}/api/auth/register`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify(userData)
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Registration failed."
    );
  }

  return data;
}


export async function loginUser(userData) {

  const response = await fetch(
    `${API_BASE_URL}/api/auth/login`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify(userData)
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Login failed."
    );
  }

  return data;
}


export async function getCurrentUser() {

  const response = await fetch(
    `${API_BASE_URL}/api/auth/me`,
    {
      headers: {
        ...getAuthHeaders()
      }
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Could not load user."
    );
  }

  return data;
}


// ==================================================
// PROFILE
// ==================================================

export async function getProfile() {

  const response = await fetch(
    `${API_BASE_URL}/api/profile`,
    {
      headers: {
        ...getAuthHeaders()
      }
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Could not load profile."
    );
  }

  return data;
}


export async function updateProfile(profileData) {

  const response = await fetch(
    `${API_BASE_URL}/api/profile`,
    {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders()
      },

      body: JSON.stringify(profileData)
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Profile update failed."
    );
  }

  return data;
}


// ==================================================
// LEAF
// ==================================================

export async function predictLeaf(file) {

  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/leaf/predict`,
    {
      method: "POST",

      headers: {
        ...getAuthHeaders()
      },

      body: formData
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Leaf prediction failed."
    );
  }

  return data;
}


// ==================================================
// FRUIT
// ==================================================

export async function predictFruit(file) {

  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/fruit/predict`,
    {
      method: "POST",

      headers: {
        ...getAuthHeaders()
      },

      body: formData
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Fruit prediction failed."
    );
  }

  return data;
}


// ==================================================
// ADVISORY
// ==================================================

export async function getAdvisory(inputData) {

  const response = await fetch(
    `${API_BASE_URL}/api/advisory`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders()
      },

      body: JSON.stringify(inputData)
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Advisory request failed."
    );
  }

  return data;
}


export async function getHistory() {

  const response = await fetch(
    `${API_BASE_URL}/api/history`,
    {
      headers: {
        ...getAuthHeaders()
      }
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Could not load history."
    );
  }

  return data;
}


export async function getDashboardWeather() {

  const response = await fetch(
    `${API_BASE_URL}/api/weather/current`,
    {
      headers: {
        ...getAuthHeaders()
      }
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Could not load weather."
    );
  }

  return data;
}