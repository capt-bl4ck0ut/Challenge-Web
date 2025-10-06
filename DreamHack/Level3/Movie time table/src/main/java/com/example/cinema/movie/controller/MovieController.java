package com.example.cinema.movie.controller;

import com.example.cinema.movie.service.MovieService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import java.io.File;
import java.io.IOException;

@Controller
public class MovieController {

    @Autowired
    private MovieService movieService;

    @GetMapping("/table")
    public String getMovieTable(Model model) {
        File file = new File("/app/tables/table.xml");
        model.addAttribute("movies", movieService.getMovies(file));
        return "table";
    }

    @PostMapping("/test")
    public String test(HttpServletRequest request, Model model) {
        try {
            model.addAttribute("movies", movieService.getMovies(request.getInputStream()));
        } catch (IOException e) {
            e.getStackTrace();
        }
        return "table";
    }
}
