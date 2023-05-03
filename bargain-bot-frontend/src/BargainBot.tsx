import React, { useEffect, useRef } from "react";
import { useSelector } from "react-redux";
import { Footer } from "./Footer";
import Header from "./Header";
import { RootState } from "./redux/store";
import "./index.css";

function BargainBot() {
  const Messages = useSelector((state: RootState) => state.TextMessage);
  const ref = useRef(null);

  useEffect(() => {
    // @ts-ignore
    ref.current?.scrollIntoView({ behavior: "smooth" });
  }, [Messages]);

  return (
    <div className="flex flex-col items-center justify-center fixed bottom-[10px] right-[10px] drop-shadow-2xl">
      <Header />
      <div className="flex flex-col justify-start w-[400px] h-[540px] border-[1px] border-slate-300  bg-slate-100 overflow-y-scroll scrollbar-hide">
        {Messages.result &&
          Messages.result.map((val: any, key: any) =>
            val.sender !== undefined ? (
              <div
                key={key}
                ref={ref}
                className="self-end border-[1px]  max-w-[320px] w-auto max-h-[200px] h-auto my-2 mx-4 py-2 px-2 rounded-t-[16px] rounded-l-[16px] bg-gradient-to-r from-pink-200 rounded-[2px to-blue-200"
              >
                <h1>{val.message}</h1>
              </div>
            ) : (
              <div
                key={key}
                ref={ref}
                className="self-start border-[1px] max-w-[320px] w-auto max-h-[200px] h-auto my-2 mx-4 py-2 px-2 rounded-t-[16px] rounded-r-[16px] bg-gradient-to-r from-[#639AE3] rounded-[2px to-[#4E7AC1]"
              >
                <h1>{val.text}</h1>
              </div>
            )
          )}
      </div>
      <Footer />
    </div>
  );
}

export default BargainBot;
