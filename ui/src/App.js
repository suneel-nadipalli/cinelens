import { useState } from "react";

import "bootstrap/dist/css/bootstrap.min.css";

import "./css/App.css";

import SearchImage from "./components/SearchImage";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5050";

const App = () => {
  const [searchType, setSearchType] = useState("title");

  return (
    <div className="App">
      <div className="overlay"></div> {/* Overlay div */}
      <div className="container">
        <p className="mb-0">Movies at your fingertips</p>
        <h1>CineLens</h1>
        <p>
          Search for you favorite movies with the bare minimum! Upload a still
          from the movie, describe a scene or just vague details you remember
          and find out that one moive that's been bugging you at the back of
          your head!
        </p>
        <nav className="nav">
          <div
            className={`nav-item ${searchType === "title" ? "active" : ""}`}
            onClick={() => setSearchType("title")}
          >
            Search by Title
            {searchType === "title" && <div className="underline"></div>}
          </div>
          <div
            className={`nav-item ${searchType === "genre" ? "active" : ""}`}
            onClick={() => setSearchType("genre")}
          >
            Search by Genre
            {searchType === "genre" && <div className="underline"></div>}
          </div>
        </nav>
        {searchType === "title" ? (
          <SearchImage></SearchImage>
        ) : (
          // <div>Search by Title Component Here</div>
          <div>Search by Genre Component Here</div>
        )}
      </div>
    </div>
  );
};

export default App;
