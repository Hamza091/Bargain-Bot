import React from "react";
import { FaOpencart } from "react-icons/fa";
import { GoSignIn } from "react-icons/go";
import { useDispatch } from "react-redux";
import { SET_ROUTE } from "./redux/reducer";

const StoreNavBar = () => {
  const dispatch = useDispatch();
  return (
    <div className="w-full h-[60px] bg-gradient-to-r from-[#4E7AC1]  via-pink-400 to-[#639AE3] shadow-xl flex items-center justify-between px-[16px]">
      <div className="flex items-center gap-1 cursor-pointer">
        <FaOpencart size={40} className="text-white" />
        <h3 className="text-white italic font-bold text-[24px]">Store!</h3>
      </div>
      <div
        onClick={() => {
          dispatch(SET_ROUTE(""));
        }}
        className="flex items-center gap-1 cursor-pointer"
      >
        <h3 className="text-white font-semibold text-[18px]">Sign in</h3>
        <GoSignIn size={20} className="text-white" />
      </div>
    </div>
  );
};

export default StoreNavBar;
