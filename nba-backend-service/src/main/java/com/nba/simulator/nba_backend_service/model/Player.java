package com.nba.simulator.nba_backend_service.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "players")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Player {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name;

    private String team;
    private String position;

    @Column(name = "pts")
    private Double pts;

    @Column(name = "reb")
    private Double reb;

    @Column(name = "ast")
    private Double ast;

    @Column(name = "stl")
    private Double stl;

    @Column(name = "blk")
    private Double blk;

    @Column(name = "tov")
    private Double tov;

    @Column(name = "ts_pct")
    private Double tsPct;

    @Column(name = "usg_pct")
    private Double usgPct;

    @Column(name = "min_per_game")
    private Double min;
}