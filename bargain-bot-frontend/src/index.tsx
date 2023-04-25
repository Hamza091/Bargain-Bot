import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import store, { RootState } from "./redux/store";
import { Provider, useSelector } from "react-redux";
import App from "./App";
import LoginPage from "./LoginPage";
import AppContainer from "./AppContainer";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <AppContainer />
    </Provider>
  </React.StrictMode>
);
