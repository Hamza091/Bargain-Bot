import React from "react";
import { product } from "./products";
const path = "./assets/images/";

const Shop = () => {
  return (
    <div className="w-full h-auto p-5">
      <h2 className="text-[28px] italic font-semibold">Grosseries</h2>
      <div className="w-full h-auto grid grid-cols-7 mx-auto">
        {product.map((val: any, key: number) => (
          <div className="w-[200px] h-[200px] border my-[16px]" key={key}>
            <h2>{val.title}</h2>
            <img
              className="w-[200px] h-[200px]"
              src={path + val.filename}
              alt=""
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Shop;
