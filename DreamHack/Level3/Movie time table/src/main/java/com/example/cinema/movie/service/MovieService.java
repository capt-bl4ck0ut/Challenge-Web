package com.example.cinema.movie.service;

import com.example.cinema.movie.exception.BadKeywordException;
import com.example.cinema.movie.model.Movie;
import org.springframework.stereotype.Service;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.io.*;
import java.util.ArrayList;
import java.util.List;

@Service
public class MovieService {

    private static final Logger logger = LoggerFactory.getLogger(MovieService.class);

    private String convertStreamToString(InputStream is) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            sb.append(line).append("\n");
        }
        return sb.toString();
    }

    public List<Movie> getMovies(File file) {
        return parseMovies(file);
    }

    public List<Movie> getMovies(InputStream inputStream) {
        return parseMovies(inputStream);
    }

    public List<Movie> parseMovies(Object source) {
        List<Movie> movies = new ArrayList<>();
        try {
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            dbFactory.setValidating( false );
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc;
            if (source instanceof File){
                doc = dBuilder.parse((File) source);
            } else if (source instanceof InputStream){

                String inputStreamString = convertStreamToString((InputStream) source);
                if (inputStreamString.contains("SYSTEM")){
                    throw new BadKeywordException("Not allowed.");
                }
                if(inputStreamString.contains("file://")){
                    throw new BadKeywordException("Not allowed.");
                }
                InputStream newInputStream = new ByteArrayInputStream(inputStreamString.getBytes());
                doc = dBuilder.parse(newInputStream);
            }else{
                throw new IllegalArgumentException("Unsupported type: " + source.getClass().getName());
            }
            doc.getDocumentElement().normalize();

            NodeList movieList = doc.getElementsByTagName("movie");
            for (int temp = 0; temp < movieList.getLength(); temp++) {
                Node movieNode = movieList.item(temp);
                if (movieNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element movieElement = (Element) movieNode;
                    Movie movie = new Movie();
                    movie.setTitle(movieElement.getElementsByTagName("title").item(0).getTextContent());

                    List<String> showtimes = new ArrayList<>();
                    NodeList showtimeList = movieElement.getElementsByTagName("showtime");
                    for (int count = 0; count < showtimeList.getLength(); count++) {
                        showtimes.add(showtimeList.item(count).getTextContent());
                    }
                    movie.setShowtimes(showtimes);
                    movies.add(movie);
                }
            }
        } catch (Exception e) {
            logger.error("ERROR: {}",e.getStackTrace());
            e.getStackTrace();
        }
        return movies;
    }
}
