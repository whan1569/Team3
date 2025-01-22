import React, { useState } from "react";
import "./ImageCard.css";

function ImageCard({ image, title }) {
  const [hovered, setHovered] = useState(false);
  const [hoverTimer, setHoverTimer] = useState(null);

  const handleMouseEnter = () => {
    const timer = setTimeout(() => setHovered(true), 1500); // 1.5초 후에 호버 상태로 전환
    setHoverTimer(timer);
  };

  const handleMouseLeave = () => {
    clearTimeout(hoverTimer); // 타이머 제거
    setHovered(false); // 호버 상태 해제
  };

  return (
    <div
      className={`movie ${hovered ? "hovered" : ""}`}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <img src={image} alt={title} className="movie-poster" />
      <div className="movie-hover">
        <img src={image} alt={title} className="hover-poster" />
        <h3>{title}</h3>
        <div className="movie-buttons">
          <button className="play-btn">▶ 재생</button>
          <button className="info-btn">ℹ️ 정보</button>
        </div>
      </div>
    </div>
  );
}

export default ImageCard;
