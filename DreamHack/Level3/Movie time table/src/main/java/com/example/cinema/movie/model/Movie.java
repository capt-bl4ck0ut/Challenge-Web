package com.example.cinema.movie.model;

import java.util.List;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Movie {
    private String title;
    private List<String> showtimes;
}
