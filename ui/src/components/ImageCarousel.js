import React, { useState } from "react";

import Carousel from "react-bootstrap/Carousel";

import Container from "react-bootstrap/Container";

import "../css/ImageCarousel.css";

const ImageCarousel = ({ data }) => {
  console.log("ImageCarousel received data:", data);

  return (
    <section id="movies">
      {/* <Container fluid> */}
      <Carousel controls={false} data-bs-theme="dark">
        {data.map((movie, idx) => {
          return (
            <Carousel.Item key={idx}>
              <img
                src={`data:image/jpeg;base64,${movie.image}`}
                alt={movie.name}
              />
              <p>Score {movie.score}</p>
            </Carousel.Item>
          );
        })}
      </Carousel>
      {/* </Container> */}
    </section>
  );
};

export default ImageCarousel;
