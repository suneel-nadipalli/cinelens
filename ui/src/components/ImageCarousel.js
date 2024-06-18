import React, { useState } from "react";

import Carousel from "react-bootstrap/Carousel";

import Container from "react-bootstrap/Container";

import AspectRatio from "@mui/joy/AspectRatio";

import "../css/ImageCarousel.css";

const ImageCarousel = ({ data }) => {
  const [index, setIndex] = useState(0);

  const handleSelect = (selectedIndex) => {
    setIndex(selectedIndex);
  };

  console.log("ImageCarousel received data:", data);

  return (
    <section id="movies">
      <Container fluid>
        <AspectRatio objectFit="contain" ratio="16/9">
          <Carousel
            controls={false}
            data-bs-theme="dark"
            activeIndex={index}
            onSelect={handleSelect}
          >
            {data.map((movie, idx) => {
              return (
                <Carousel.Item key={idx} style={{ height: "40rem" }}>
                  <img
                    src={`data:image/jpeg;base64,${movie.image}`}
                    alt={movie.name}
                  />
                  <p>Score {movie.score}</p>
                </Carousel.Item>
              );
            })}
          </Carousel>
        </AspectRatio>
      </Container>
    </section>
  );
};

export default ImageCarousel;
