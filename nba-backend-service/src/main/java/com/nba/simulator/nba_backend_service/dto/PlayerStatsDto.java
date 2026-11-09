package com.nba.simulator.nba_backend_service.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;  
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PlayerStatsDto {
    private String name;

    @JsonProperty("PTS")
    private Double pts;

    @JsonProperty("REB")
    private Double reb;

    @JsonProperty("AST")
    private Double ast;

    @JsonProperty("STL")
    private Double stl;

    @JsonProperty("BLK")
    private Double blk;

    @JsonProperty("TOV")
    private Double tov;

    @JsonProperty("TS_PCT")
    private Double tsPct;

    @JsonProperty("USG_PCT")
    private Double usgPct;

    @JsonProperty("MIN")
    private Double min;
}