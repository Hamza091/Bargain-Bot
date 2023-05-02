import React, { useEffect } from "react";
import StoreNavBar from "./StoreNavBar";
import Carousel from "./Carousel";
import Shop from "./Shop";
import axios from "axios";

const Store = () => {
  useEffect(() => {
    axios.post("http://localhost:5000/data", {
      obj: {
        name: "Askari",
        age: 34,
      },
    });
  }, []);
  return (
    <div className="flex items-start flex-col">
      <StoreNavBar />
      <Carousel />
      <Shop />
    </div>
  );
};

export default Store;
