import React, { useState, useEffect } from "react";
import "./WeatherWidget.css";

const WeatherWidget = () => {
  const [location, setLocation] = useState(null); // 위치 상태
  const [weatherData, setWeatherData] = useState(null); // 날씨 데이터 상태
  const [error, setError] = useState(null); // 에러 상태

  const OpenWeatherAPI = import.meta.env.VITE_OpenWeather_Key; // 환경 변수에서 API 키 가져오기

  useEffect(() => {
    // 사용자 위치 가져오기
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({
          lat: position.coords.latitude,
          lon: position.coords.longitude,
        });
      },
      (err) => {
        setError("위치 정보를 가져올 수 없습니다.");
      }
    );
  }, []);

  useEffect(() => {
    // 위치가 설정되면 날씨 데이터 가져오기
    if (location) {
      const fetchWeather = async () => {
        try {
          const response = await fetch(
            `https://api.openweathermap.org/data/2.5/weather?lat=${location.lat}&lon=${location.lon}&units=metric&appid=${OpenWeatherAPI}`
          );
          if (!response.ok) {
            throw new Error("날씨 정보를 가져오는데 실패했습니다.");
          }
          const data = await response.json();
          setWeatherData(data);
        } catch (err) {
          setError("날씨 정보를 가져오는데 실패했습니다.");
        }
      };

      fetchWeather();
    }
  }, [location, OpenWeatherAPI]);

  if (error) {
    return <div className="weather-widget">{error}</div>;
  }

  if (!weatherData) {
    return <div className="weather-widget">로딩 중...</div>;
  }

  const { main, weather } = weatherData;
  const temperature = Math.round(main.temp);
  const weatherIcon = `http://openweathermap.org/img/wn/${weather[0].icon}@2x.png`;

  return (
    <div className="weather-widget">
      <img src={weatherIcon} alt="weather icon" />
      <span className="Temperature">{temperature}°C</span>
    </div>
  );
};

export default WeatherWidget;
