import React, { useEffect, useState } from "react";
import { FiSearch } from "react-icons/fi";
import "./Search.css";
import axios from "axios";

const Search = () => {
  const [query, setQuery] = useState("");
  const [trending, setTrending] = useState([]);
  const [filteredContents, setFilteredContents] = useState([]);

  // TMDB API key (본인의 키로 대체)
  const API_KEY = "YOUR_TMDB_API_KEY";

  // 금주의 인기 콘텐츠 가져오기
  useEffect(() => {
    const fetchTrending = async () => {
      try {
        const response = await axios.get(
          `https://api.themoviedb.org/3/trending/all/week?api_key=${API_KEY}&language=ko-KR`
        );
        setTrending(response.data.results);
      } catch (error) {
        console.error("Error fetching trending data:", error);
      }
    };

    fetchTrending();
  }, []);

  // 검색 필터링
  useEffect(() => {
    if (query.trim() === "") {
      setFilteredContents([]);
      return;
    }

    const filtered = trending.filter((item) =>
      item.title
        ? item.title.toLowerCase().includes(query.toLowerCase())
        : item.name.toLowerCase().includes(query.toLowerCase())
    );
    setFilteredContents(filtered);
  }, [query, trending]);

  return (
    <div className="search">
      <div className="search-bar">
        <input
          type="text"
          placeholder="제목, 장르, 배우로 검색해보세요"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button className="search-button"><FiSearch /></button>
      </div>

      <div className="genres">
        <button>예능</button>
        <button>드라마</button>
        <button>영화</button>
        <button>범죄</button>
      </div>

      <div className="trending-section">
        <h2>금주의 인기 콘텐츠</h2>
        <div className="trending-grid">
          {(query ? filteredContents : trending).map((item, index) => (
            <div key={item.id} className="trending-item">
              <span className="rank">{index + 1}</span>
              <img
                src={`https://image.tmdb.org/t/p/w500${item.poster_path}`}
                alt={item.title || item.name}
              />
              <p className="title">{item.title || item.name}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Search;
