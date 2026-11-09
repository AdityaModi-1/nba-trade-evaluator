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
public class TradeResponseDto {
    @JsonProperty("team_a_total_impact")
    private Double teamATotalImpact;

    @JsonProperty("team_b_total_impact")
    private Double teamBTotalImpact;

    @JsonProperty("impact_differential")
    private Double impactDifferential;

    @JsonProperty("fairness_score")
    private Double fairnessScore;

    private String verdict;

    @JsonProperty("team_a_breakdown")
    private List<EvaluatedPlayerDto> teamABreakdown;

    @JsonProperty("team_b_breakdown")
    private List<EvaluatedPlayerDto> teamBBreakdown;

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class EvaluatedPlayerDto {
        private String name;

        @JsonProperty("predicted_impact")
        private Double predictedImpact;
    }
}