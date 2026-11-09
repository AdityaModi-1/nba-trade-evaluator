package com.nba.simulator.nba_backend_service.service;

import com.nba.simulator.nba_backend_service.dto.PlayerStatsDto;
import com.nba.simulator.nba_backend_service.dto.SimpleTradeRequestDto;
import com.nba.simulator.nba_backend_service.dto.TradeRequestDto;
import com.nba.simulator.nba_backend_service.dto.TradeResponseDto;
import com.nba.simulator.nba_backend_service.model.Player;
import com.nba.simulator.nba_backend_service.repository.PlayerRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.List;

@Service
@RequiredArgsConstructor
public class MlEvaluationService {

    private final RestClient mlRestClient;
    private final PlayerRepository playerRepository;

    public TradeResponseDto evaluateTrade(TradeRequestDto request) {
        return mlRestClient.post()
                .uri("/api/ml/evaluate-trade")
                .contentType(MediaType.APPLICATION_JSON)
                .body(request)
                .retrieve()
                .body(TradeResponseDto.class);
    }

    public TradeResponseDto evaluateTradeByName(SimpleTradeRequestDto request) {
        List<PlayerStatsDto> teamAStats = request.getTeamAPlayerNames().stream()
                .map(this::fetchPlayerAsDto)
                .toList();

        List<PlayerStatsDto> teamBStats = request.getTeamBPlayerNames().stream()
                .map(this::fetchPlayerAsDto)
                .toList();

        TradeRequestDto fullRequest = TradeRequestDto.builder()
                .teamAGiving(teamAStats)
                .teamBGiving(teamBStats)
                .build();

        return evaluateTrade(fullRequest);
    }

    private PlayerStatsDto fetchPlayerAsDto(String playerName) {
        Player player = playerRepository.findByNameIgnoreCase(playerName)
                .orElseThrow(() -> new IllegalArgumentException("Player not found in database: " + playerName));

        return PlayerStatsDto.builder()
                .name(player.getName())
                .pts(player.getPts())
                .reb(player.getReb())
                .ast(player.getAst())
                .stl(player.getStl())
                .blk(player.getBlk())
                .tov(player.getTov())
                .tsPct(player.getTsPct())
                .usgPct(player.getUsgPct())
                .min(player.getMin())
                .build();
    }
}