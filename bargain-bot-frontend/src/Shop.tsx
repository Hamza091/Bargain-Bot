import { product } from "./products";

const Shop = () => {
  return (
    <div className="w-full h-auto p-5">
      <h2 className="text-[28px] italic font-semibold">Grosseries</h2>
      <div className="w-full h-auto grid grid-cols-4 mx-auto">
        {product.map((val: any, key: number) => (
          <div
            className="w-auto h-[450px] mx-4 border my-[25px] rounded-md shadow-xl bg-white cursor-pointer"
            key={key}
          >
            <div className="flex p-5 object-fill w-[100%] h-auto">
              <img
                className="h-[300px] object-fill w-[100%] rounded-md"
                src={require(`./assets/images/${key}.jpg`)}
                alt=""
              />
            </div>
            <div className="px-5 h-[110px] flex items-start justify-between flex-col pb-5">
              <div>
                <h1 className="text-[14px] font-bold">{val.title}</h1>
                <h5 className="text-[11px] italic overflow-clip">
                  {val.description}
                </h5>
              </div>
              <h5>Rs. {Math.round(val.price * 10)}</h5>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Shop;
