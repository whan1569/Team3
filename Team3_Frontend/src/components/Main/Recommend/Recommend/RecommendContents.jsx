import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import "./RecommendContents.css";

const API_KEY = import.meta.env.VITE_TMDB_API;
const imageUrl = "https://image.tmdb.org/t/p/original";

function RecommendContents() {
  const [movies, setMovies] = useState([]);
  const sectionRefs = useRef([]);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await axios.get(
          `https://api.themoviedb.org/3/movie/top_rated?api_key=${API_KEY}&language=ko-KO`
        );
        const validMovies = response.data.results
          .filter((movie) => movie.poster_path && movie.title)
          .map((movie) => ({
            image: `${imageUrl}${movie.poster_path}`,
            title: movie.title,
          }));
        setMovies(validMovies.slice(0, 20));
      } catch (error) {
        console.error("영화를 가져오는 중 오류 발생:", error);
      }
    };

    fetchMovies();
  }, []);

  const scrollLeft = (index) => {
    sectionRefs.current[index].scrollBy({
      left: -300,
      behavior: "smooth",
    });
  };

  const scrollRight = (index) => {
    sectionRefs.current[index].scrollBy({
      left: 300,
      behavior: "smooth",
    });
  };

  return (
    <div className="recommend_contents">
      <h2 className="section_title">회원님을 위해 엄선한 콘텐츠</h2>
      <div className="slider_wrapper">
        <button
          className="scroll_button left"
          onClick={() => scrollLeft(0)}
        >
          &lt;
        </button>
        <div className="slider_container" ref={(el) => (sectionRefs.current[0] = el)}>
          {movies.map((movie, index) => (
            <div key={index} className="movie_card">
              <img src={movie.image} alt={movie.title} className="movie_image" />
              <div className="movie_hover">
                <div className="movie_title">{movie.title}</div>
                <div className="movie_buttons">
                  <button className="play_btn">▶ 재생</button>
                  <button className="info_btn">ℹ️ 정보</button>
                </div>
              </div>
            </div>
          ))}
        </div>
        <button
          className="scroll_button right"
          onClick={() => scrollRight(0)}
        >
          &gt;
        </button>
      </div>

      {[1, 2, 3, 4].map((sectionIndex) => (
        <React.Fragment key={sectionIndex}>
          <h2 className="section_title">추천 리스트 {sectionIndex}</h2>
          <div className="slider_wrapper">
            <button
              className="scroll_button left"
              onClick={() => scrollLeft(sectionIndex)}
            >
              &lt;
            </button>
            <div
              className="slider_container"
              ref={(el) => (sectionRefs.current[sectionIndex] = el)}
            >
              {movies.map((movie, index) => (
                <div key={index} className="movie_card">
                  <img src={movie.image} alt={movie.title} className="movie_image" />
                  <div className="movie_hover">
                    <div className="movie_title">{movie.title}</div>
                    <div className="movie_buttons">
                      <button className="play_btn">▶ 재생</button>
                      <button className="info_btn">ℹ️ 정보</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <button
              className="scroll_button right"
              onClick={() => scrollRight(sectionIndex)}
            >
              &gt;
            </button>
          </div>
        </React.Fragment>
      ))}
    </div>
  );
}

export default RecommendContents;
