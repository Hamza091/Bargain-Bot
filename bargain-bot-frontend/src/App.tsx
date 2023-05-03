import BargainBot from "./BargainBot";
import { BsChatTextFill } from "react-icons/bs";
import { useDispatch, useSelector } from "react-redux";
import { SET_BOTPOPUP } from "./redux/reducer";
import { RootState } from "./redux/store";
import Store from "./Store";

const App = () => {
  const isBotOpen = useSelector((state: RootState) => state.Buttons.botPopUp);
  const dispatch = useDispatch();
  return (
    <div className="w-full h-auto">
      <Store />
      {!isBotOpen && (
        <div
          onClick={() => dispatch(SET_BOTPOPUP(true))}
          className="rounded-full animate-bounce fixed z-10 bottom-[20px] cursor-pointer shadow-xl right-[20px] w-[60px] h-[60px] bg-gradient-to-r from-[#4E7AC1]  via-pink-400 to-[#639AE3] flex items-center justify-center"
        >
          <BsChatTextFill
            size={40}
            className="text-white w-[40px] h-[40px] object-fill cursor-pointer"
          />
        </div>
      )}

      {isBotOpen && <BargainBot />}
    </div>
  );
};

export default App;
