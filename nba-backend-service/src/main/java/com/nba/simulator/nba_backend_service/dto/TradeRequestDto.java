package com.nba.simulator.nba_backend_service.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TradeRequestDto {
    @JsonProperty("team_a_giving")
    private List<PlayerStatsDto> teamAGiving;

    @JsonProperty("team_b_giving")
    private List<PlayerStatsDto> teamBGiving;
}