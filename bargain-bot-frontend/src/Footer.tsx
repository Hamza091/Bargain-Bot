import axios from "axios";
import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import SendIcon from "./assets/SendIcon.svg";
import { SET_RESPONSE, SET_TEXTMESSGAGE } from "./redux/reducer";
import { RootState } from "./redux/store";

export const Footer = () => {
  const text = useSelector((state: RootState) => state.TextMessage.text);
  const [typedMessage, setTypedMessage] = useState("");
  const dispatch = useDispatch();

  const SendMessage = async () => {
    console.log(text);
    let data = {
      sender: "Askari",
      message: text,
    };

    dispatch(SET_RESPONSE(data));

    await axios
      .post("http://localhost:5005/webhooks/rest/webhook", data)
      .then((result) => {
        console.log(result.data);
        result.data.map((val: any, key: any) => {
          if (val.text) {
            dispatch(
              SET_RESPONSE({
                text: val.text,
                recipient_id: val.recipient,
              })
            );
            console.log(val.text);
          }
        });
      });
  };

  return (
    <div className="flex border-[1px] border-t-[0px] items-center justify-between px-4 w-[400px] bg-slate-200 border-slate-300 h-[56px] rounded-b-[4px] ">
      <div className="h-[42px] flex items-center justify-center bg-gradient-to-r from-[#4E7AC1] rounded-[2px] via-pink-400 w-[310px] to-[#639AE3]">
        <input
          value={typedMessage}
          onChange={(e) => {
            setTypedMessage(e.target.value);
            dispatch(SET_TEXTMESSGAGE(e.target.value));
          }}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              SendMessage();
              setTypedMessage("");
            }
          }}
          className="h-[36px] w-[304px] rounded-[3px] outline-none px-2"
          type="text"
          placeholder="Talk to Chatbot..."
        />
      </div>
      <div
        onClick={() => {
          SendMessage();
          setTypedMessage("");
        }}
        className="flex items-center justify-center cursor-pointer rounded-full w-[46px] h-[46px] overflow-hidden bg-gradient-to-r from-[#4E7AC1] via-pink-400 to-[#639AE3]"
      >
        <img
          className="w-[40px] border-[2px] border-white rounded-full"
          src={SendIcon}
          alt="Send Icon"
        />
      </div>
    </div>
  );
};
