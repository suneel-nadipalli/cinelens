import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./css/App.css";
import SearchImage from "./components/SearchImage";
import ResultsCarousel from "./components/ResultsCarousel";
import SearchDetails from "./components/SearchDetails";
import { Row, Col } from "react-bootstrap";

const App = () => {
  const [searchType, setSearchType] = useState("title");

  const [similarImages, setSimilarImages] = useState([]);

  const handleSimilarImages = (data) => {
    console.log("Received similar images data:", data); // Debugging log
    setSimilarImages(data);
  };

  useEffect(() => {
    console.log("similarImages state updated:", similarImages);
  }, [similarImages]);

  return (
    <div className="App">
      <div className="overlay"></div>
      <Row>
        <Col>
          <div className="container">
            <p className="mb-0">Movies at your fingertips</p>
            <h1>CineLens</h1>
            <p style={{ margin: "20px" }}>
              Search for your favorite movies with the bare minimum! Upload a
              still from the movie, describe a scene or just vague details you
              remember and find out that one movie that's been bugging you at
              the back of your head!
            </p>
            <nav className="nav">
              <div
                className={`nav-item ${searchType === "title" ? "active" : ""}`}
                onClick={() => setSearchType("title")}
              >
                Search by Image
                {searchType === "title" && <div className="underline"></div>}
              </div>
              <div
                className={`nav-item ${searchType === "genre" ? "active" : ""}`}
                onClick={() => setSearchType("genre")}
              >
                Search by Plot/Details
                {searchType === "genre" && <div className="underline"></div>}
              </div>
            </nav>
            <div className="search-content">
              {searchType === "title" ? (
                <>
                  <SearchImage onSimilarImages={handleSimilarImages} />
                </>
              ) : (
                <>
                  <SearchDetails onSimilarImages={handleSimilarImages} />
                </>
              )}
            </div>
          </div>
        </Col>
        <Col style={{ zIndex: 2 }}>
          {similarImages.length > 0 && (
            <ResultsCarousel data={similarImages}></ResultsCarousel>
          )}
        </Col>
      </Row>
    </div>
  );
};

export default App;
