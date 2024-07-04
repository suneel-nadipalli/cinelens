import React, { useState } from "react";

import { Row, Col, Form, Button } from "react-bootstrap";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5050";

const SearchDetails = ({ onSimilarImages }) => {
  const [text, setText] = useState("");

  const handleOnSubmit = (event) => {
    event.preventDefault();

    console.log("Text:", text);

    const text_data = {
      text: text,
    };

    fetch(`${API_URL}/text_rag`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(text_data),
    })
      .then((response) => response.json())
      .then((data) => {
        onSimilarImages(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <Row className="justify-content-center">
      <Col xs={12} md={8}>
        <Form onSubmit={handleOnSubmit}>
          <Row>
            <Col xs={9}>
              <Form.Control
                type="text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="What do you remember about the movie?"
              />
            </Col>
            <Col>
              <Button variant="primary" type="submit">
                Search
              </Button>
            </Col>
          </Row>
        </Form>
      </Col>
    </Row>
  );
};

export default SearchDetails;
