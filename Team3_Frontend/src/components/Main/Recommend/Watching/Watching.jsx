import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import "./Watching.css";

const API_KEY = import.meta.env.VITE_TMDB_API;
const imageUrl = "https://image.tmdb.org/t/p/original";

function Watching() {
  const [movies, setMovies] = useState([]);
  const sliderRef = useRef(null);

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

  const scrollSlider = (direction) => {
    const scrollAmount = sliderRef.current.offsetWidth / 2;
    sliderRef.current.scrollLeft += direction === "left" ? -scrollAmount : scrollAmount;
  };

  return (
    <div className="watching">
      <h2 className="title">금주의 TOP 20</h2>
      <div className="slider-container">
        <button className="slider-btn left" onClick={() => scrollSlider("left")}>
          &lt;
        </button>
        <div className="slider" ref={sliderRef}>
          {movies.map((movie, index) => (
            <div key={movie.id} className="movie">
              <div className="rank">{index + 1}</div>
              <img
                src={`${imageUrl}${movie.poster_path}`}
                alt={movie.title}
                className="movie-poster"
              />
              <div className="movie-hover">
                <img
                  src={`${imageUrl}${movie.poster_path}`}
                  alt={movie.title}
                  className="hover-poster"
                />
                <h3>{movie.title}</h3>
                <div className="movie-buttons">
                  <button className="play-btn">▶ 재생</button>
                  <button className="info-btn">ℹ️ 정보</button>
                </div>
              </div>
            </div>
          ))}
        </div>
        <button className="slider-btn right" onClick={() => scrollSlider("right")}>
          &gt;
        </button>
      </div>
    </div>
  );
}

export default Watching;
