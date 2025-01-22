import React, { useEffect, useState } from 'react';
import axios from '../../../axios';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './Banner.css';

const API_KEY = import.meta.env.VITE_TMDB_API;
const imageUrl = 'https://image.tmdb.org/t/p/original';

function Banner() {
    const [movies, setMovies] = useState([]);

    useEffect(() => {
        axios
            .get(`trending/all/week?api_key=${API_KEY}&language=ko-KO`)
            .then((response) => {
                const validMovies = response.data.results.filter(
                    (movie) => movie.backdrop_path
                );
                setMovies(validMovies.slice(0, 5));
            })
            .catch((error) => {
                console.error('Error fetching movies:', error);
            });
    }, []);

    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        arrows: true,
    };

    return (
        <div className="banner">
            <Slider {...settings}>
                {movies.map((movie) => (
                    <div key={movie.id} className="slide">
                        <img
                            src={`${imageUrl + movie.backdrop_path}`}
                            alt={movie.title || movie.original_name}
                            className="slide-image"
                        />
                        <div className="content">
                            <h1 className="title">{movie.original_name || movie.title}</h1>
                            <div className="banner_buttons">
                                <button className="button">Play</button>
                                <button className="button">My List</button>
                            </div>
                            <h1 className="description">{movie.overview}</h1>
                        </div>
                        <div className="fade_bottom"></div>
                    </div>
                ))}
            </Slider>
        </div>
    );
}

export default Banner;
