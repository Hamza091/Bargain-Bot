import React from "react";
import { useDispatch } from "react-redux";
import { SET_BOTPOPUP } from "./redux/reducer";

const Header = () => {
  const dispatch = useDispatch();
  return (
    <div className="flex border-b-[1px] items-center justify-between px-4 w-[400px] bg-slate-300 border-slate-400 h-[48px] rounded-t-[4px] bg-gradient-to-r from-[#4E7AC1] rounded-[2px] via-pink-400 to-[#639AE3]">
      <h1 className="font-bold text-[22px] text-white">Bargain Bot</h1>
      <div
        onClick={() => dispatch(SET_BOTPOPUP(false))}
        className="flex items-center justify-center w-[20px] h-[20px] rounded-[4px] cursor-pointer"
      >
        <div className="w-[20px] bg-white h-[4px]"></div>
      </div>
    </div>
  );
};

export default Header;
