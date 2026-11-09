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
public class SimpleTradeRequestDto {

    @JsonProperty("team_a_player_names")
    private List<String> teamAPlayerNames;

    @JsonProperty("team_b_player_names")
    private List<String> teamBPlayerNames;
}