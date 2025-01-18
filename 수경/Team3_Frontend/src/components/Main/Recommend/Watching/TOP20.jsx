import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import ImageCard from "./ImageCard";
import "./TOP20.css";

const API_KEY = import.meta.env.VITE_TMDB_API;
const imageUrl = "https://image.tmdb.org/t/p/original";

function TOP20() {
  const [movies, setMovies] = useState([]);
  const sliderRef = useRef(null);
  const isDragging = useRef(false);
  const startX = useRef(0);
  const scrollLeft = useRef(0);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await axios.get(
          `https://api.themoviedb.org/3/movie/top_rated?api_key=${API_KEY}&language=ko-KO`
        );
        const validMovies = response.data.results.filter((movie) => movie.poster_path);
        setMovies(validMovies);
      } catch (error) {
        console.error("Error fetching movies:", error);
      }
    };

    fetchMovies();
  }, []);

  const handleMouseDown = (e) => {
    isDragging.current = true;
    startX.current = e.pageX - sliderRef.current.offsetLeft;
    scrollLeft.current = sliderRef.current.scrollLeft;
    sliderRef.current.style.cursor = "grabbing";
  };

  const handleMouseMove = (e) => {
    if (!isDragging.current) return;
    e.preventDefault();
    const x = e.pageX - sliderRef.current.offsetLeft;
    const walk = (x - startX.current) * 1.5; // 스크롤 속도 조정
    sliderRef.current.scrollLeft = scrollLeft.current - walk;
  };

  const handleMouseUpOrLeave = () => {
    isDragging.current = false;
    sliderRef.current.style.cursor = "grab";
  };

  return (
    <div className="watching">
      <h2 className="title">금주의 TOP 20</h2>
      <div
        className="slider-container"
        ref={sliderRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUpOrLeave}
        onMouseLeave={handleMouseUpOrLeave}
      >
        {movies.map((movie, index) => (
          <ImageCard
            key={movie.id}
            rank={index + 1}
            image={`${imageUrl}${movie.poster_path}`}
            title={movie.title}
          />
        ))}
      </div>
    </div>
  );
}

export default TOP20;
