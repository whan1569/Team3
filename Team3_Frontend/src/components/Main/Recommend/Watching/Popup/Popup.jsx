import React from "react";
import "./Popup.css";

function Popup({ movie, onClose }) {
  if (!movie) return null;

  return (
    <div className="popup_overlay" onClick={onClose}>
      <div className="popup_content" onClick={(e) => e.stopPropagation()}>
        <button className="popup_close" onClick={onClose}>
          &times;
        </button>
        <div
          className="popup_background"
          style={{ backgroundImage: `url(${movie.image})` }}
        ></div>
        <div className="popup_gradient"></div>
        <div className="popup_details">
          <h2>{movie.title}</h2>
          <p>{movie.overview || "설명이 없습니다."}</p>
        </div>
      </div>
    </div>
  );
}

export default Popup;
