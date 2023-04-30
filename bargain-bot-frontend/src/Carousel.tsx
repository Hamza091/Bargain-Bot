import React, { useEffect, useState } from "react";
import Carousel from "react-bootstrap/Carousel";
import img1 from "./assets/supermarket-banner-concept-with-ingredients (1).jpg";
import img2 from "./assets/supermarket-banner-concept-with-ingredients (2).jpg";
import img3 from "./assets/supermarket-banner-concept-with-ingredients.jpg";
import {
  BsFillArrowLeftCircleFill,
  BsFillArrowRightCircleFill,
} from "react-icons/bs";

const Carousel1 = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const images = [img1, img2, img3];

  const handlePrev = () => {
    if (currentIndex === 0) {
      setCurrentIndex(images.length - 1);
    } else {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleNext = () => {
    if (currentIndex === images.length - 1) {
      setCurrentIndex(0);
    } else {
      setCurrentIndex(currentIndex + 1);
    }
  };

  useEffect(() => {
    const timer = setInterval(() => {
      handleNext();
    }, 2000);
    return () => clearInterval(timer);
  }, [currentIndex]);

  return (
    <div className="carousel w-full p-5">
      <img
        className="w-full animate-pulse"
        src={images[currentIndex]}
        alt="Carousel item"
      />
      <div className="carousel-buttons">
        <button
          className="absolute left-10 top-[380px] cursor-pointer"
          onClick={handlePrev}
        >
          <BsFillArrowLeftCircleFill size={40} />
        </button>
        <button
          className="absolute right-10 top-[380px] cursor-pointer"
          onClick={handleNext}
        >
          <BsFillArrowRightCircleFill size={40} />
        </button>
      </div>
    </div>
  );
};

export default Carousel1;
