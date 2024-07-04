import React, { useState } from "react";

import Carousel from "react-bootstrap/Carousel";

import Container from "react-bootstrap/Container";

import { Row, Col } from "react-bootstrap";

import { Rating } from "@smastrom/react-rating";

import { SiHbo } from "react-icons/si";

import { TbBrandDisney } from "react-icons/tb";

import { SiPrime } from "react-icons/si";

import { RiNetflixFill } from "react-icons/ri";

import { BsYoutube } from "react-icons/bs";

import Badge from "react-bootstrap/Badge";

import "@smastrom/react-rating/style.css";

import Stack from "react-bootstrap/Stack";

import "../css/ResultsCarousel.css";

const ResultsCarousel = ({ data }) => {
  const [index, setIndex] = useState(0);

  const handleSelect = (selectedIndex) => {
    setIndex(selectedIndex);
  };

  return (
    <section id="movies">
      <Carousel
        // data-bs-theme="dark"
        activeIndex={index}
        onSelect={handleSelect}
      >
        {data.map((movie, movie_idx) => {
          const genres = movie.genres;
          const providers = movie.providers;
          return (
            <Carousel.Item key={movie_idx}>
              <Container
                fluid
                style={{
                  backgroundColor: "black",
                  borderBlockColor: "blue",
                  borderRadius: "10px",
                  // width: "950px",
                }}
              >
                <Row>
                  <Col
                    style={{
                      margin: "30px",
                      textAlign: "left",
                      color: "white",
                    }}
                  >
                    <p
                      style={{
                        fontSize: "30px",
                        color: "white",
                        marginTop: "-10px",
                      }}
                    >
                      {movie.title}
                    </p>
                    <p
                      style={{
                        fontSize: "15px",
                        color: "white",
                        marginTop: "-10px",
                      }}
                    >
                      {movie.runtime} min | {movie.release_date}
                    </p>
                    <Rating
                      style={{ maxWidth: 125, marginTop: "-10px" }}
                      value={movie.rating}
                      readOnly={true}
                    />
                    <p style={{ color: "white", marginTop: "15px" }}>
                      {movie.overview}
                    </p>
                    <Stack direction="horizontal" gap={2}>
                      {genres.map((genre, idx) => {
                        return (
                          <Badge
                            key={idx}
                            bg="primary"
                            style={{ color: "white" }}
                          >
                            {genre}
                          </Badge>
                        );
                      })}
                    </Stack>
                    <Stack
                      direction="horizontal"
                      gap={3}
                      style={{ marginTop: "10px" }}
                    >
                      {providers.map((provider, idx) => {
                        if (provider === "max") {
                          return <SiHbo key={idx} size={30} color="white" />;
                        } else if (provider === "disney") {
                          return (
                            <TbBrandDisney key={idx} size={30} color="white" />
                          );
                        } else if (provider === "prime") {
                          return <SiPrime key={idx} size={30} color="white" />;
                        } else if (provider === "netflix") {
                          return (
                            <RiNetflixFill key={idx} size={30} color="white" />
                          );
                        } else if (provider === "youtube") {
                          return (
                            <BsYoutube key={idx} size={30} color="white" />
                          );
                        }
                      })}
                    </Stack>
                  </Col>
                  <Col>
                    <img
                      src={movie.poster}
                      alt={movie.name}
                      style={{ height: "600px", padding: "20px" }}
                    />
                    {/* <Carousel.Caption>{movie.tagline}</Carousel.Caption> */}
                  </Col>
                </Row>
              </Container>
            </Carousel.Item>
          );
        })}
      </Carousel>
    </section>
  );
};

export default ResultsCarousel;
