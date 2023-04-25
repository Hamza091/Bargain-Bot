import React, { useState } from "react";
import TextField from "@mui/material/TextField";
import { Button } from "@mui/material";
import { useDispatch } from "react-redux";
import { SET_ROUTE } from "./redux/reducer";

const LoginPage = () => {
  const [userName, setUserName] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const dispatch = useDispatch();
  return (
    <div className="absolute top-1/2 left-1/2 border h-auto w-[400px] flex items-center justify-center flex-col -translate-x-1/2 -translate-y-1/2 px-[16px] py-[8px] rounded-[5px] shadow-2xl">
      <h3 className="font-bold text-[24px] mt-[16px]">Welcome to Store!</h3>
      <div className="mt-[16px]">
        <TextField
          onChange={(e) => setUserName(e.target.value)}
          className="w-[350px] bg-[#E8F0FE]"
          id="outlined-basic"
          label="Username"
          variant="outlined"
        />
      </div>
      <div className="mt-[16px]">
        <TextField
          onChange={(e) => setPassword(e.target.value)}
          className="w-[350px] bg-[#E8F0FE]"
          id="outlined-basic"
          label="Password"
          type="password"
          variant="outlined"
        />
      </div>
      <div
        onClick={() => {
          console.log(userName, password);
          dispatch(SET_ROUTE("/store"));
        }}
        className="my-[16px]"
      >
        <Button variant="contained">Login</Button>
      </div>
    </div>
  );
};

export default LoginPage;
