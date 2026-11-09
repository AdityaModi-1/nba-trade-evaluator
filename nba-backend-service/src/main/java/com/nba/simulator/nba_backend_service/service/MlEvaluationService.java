package com.nba.simulator.nba_backend_service.service;

import com.nba.simulator.nba_backend_service.dto.TradeRequestDto;
import com.nba.simulator.nba_backend_service.dto.TradeResponseDto;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
@RequiredArgsConstructor
public class MlEvaluationService {

    private final RestClient mlRestClient;

    public TradeResponseDto evaluateTrade(TradeRequestDto request) {
        return mlRestClient.post()
                .uri("/api/ml/evaluate-trade")
                .contentType(MediaType.APPLICATION_JSON)
                .body(request)
                .retrieve()
                .body(TradeResponseDto.class);
    }
}