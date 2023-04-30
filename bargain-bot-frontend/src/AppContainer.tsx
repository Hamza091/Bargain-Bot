import React from "react";
import { useSelector } from "react-redux";
import { RootState } from "./redux/store";
import LoginPage from "./LoginPage";
import App from "./App";

const AppContainer = () => {
  const route = useSelector((state: RootState) => state.Router.route);
  return (
    <div>
      {route === "" && <LoginPage />}
      {route === "/store" && <App />}
    </div>
  );
};

export default AppContainer;
