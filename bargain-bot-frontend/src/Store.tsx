import React from "react";
import StoreNavBar from "./StoreNavBar";
import Carousel from "./Carousel";
import Shop from "./Shop";

const Store = () => {
  return (
    <div className="flex items-start flex-col">
      <StoreNavBar />
      <Carousel />
      <Shop />
    </div>
  );
};

export default Store;
