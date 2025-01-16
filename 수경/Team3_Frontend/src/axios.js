import axios from 'axios'

const baseUrl =  'https://api.themoviedb.org/3';

const instance = axios.create({
    baseURL: baseUrl,
});

export default instance ;