import { useState } from "react";

import "bootstrap/dist/css/bootstrap.min.css";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5050";

function App() {
  const [file, setFile] = useState();
  function handleChange(e) {
    e.preventDefault();
    console.log(e.target.files);
    setFile(URL.createObjectURL(e.target.files[0]));

    const img_data = new FormData();

    img_data.append("image", e.target.files[0]);

    fetch(`${API_URL}/describe_img`, {
      method: "POST",
      body: img_data,
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
      });
  }

  return (
    <div>
      <h2>Add Image:</h2>
      <input type="file" onChange={handleChange} />
      <img src={file} alt="" />
    </div>
  );
}

export default App;
