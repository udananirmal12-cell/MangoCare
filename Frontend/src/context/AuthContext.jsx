import {
  createContext,
  useContext,
  useEffect,
  useState
} from "react";

import {
  getCurrentUser,
  loginUser,
  registerUser
} from "../services/api";


const AuthContext = createContext(null);


export function AuthProvider({
  children
}) {

  const [user, setUser] =
    useState(null);

  const [loading, setLoading] =
    useState(true);


  useEffect(() => {

    const token =
      localStorage.getItem(
        "mangocare_token"
      );

    if (!token) {

      setLoading(false);

      return;
    }


    loadUser();

  }, []);


  async function loadUser() {

    try {

      const data =
        await getCurrentUser();

      setUser(data);

    } catch (error) {

      localStorage.removeItem(
        "mangocare_token"
      );

      setUser(null);

    } finally {

      setLoading(false);

    }
  }


  async function login(
    email,
    password
  ) {

    const data =
      await loginUser({
        email,
        password
      });


    localStorage.setItem(
      "mangocare_token",
      data.access_token
    );


    setUser(
      data.user
    );


    return data;
  }


  async function register(
    name,
    email,
    password
  ) {

    const data =
      await registerUser({
        name,
        email,
        password
      });

    return data;
  }


  function logout() {

    localStorage.removeItem(
      "mangocare_token"
    );

    setUser(null);
  }


  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        loading,
        login,
        register,
        logout,
        loadUser
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}


export function useAuth() {

  return useContext(
    AuthContext
  );
}