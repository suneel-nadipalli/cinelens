import React, { useState } from "react";
import "../css/SearchImage.css";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5050";

const SearchImage = ({ onSimilarImages }) => {
  const [selectedImage, setSelectedImage] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(URL.createObjectURL(file));

      const img_data = new FormData();

      img_data.append("image", file);

      fetch(`${API_URL}/img_rag`, {
        method: "POST",
        body: img_data,
      })
        .then((response) => response.json())
        .then((data) => {
          onSimilarImages(data);
          // console.log(data);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  };

  return (
    <div className="image-upload">
      <input type="file" accept="image/*" onChange={handleImageUpload} />
      {/* {imageName && <p className="image-name">{imageName}</p>} */}
      {selectedImage && (
        <div className="image-preview">
          <img src={selectedImage} alt="Uploaded preview" />
        </div>
      )}
    </div>
  );
};

export default SearchImage;
