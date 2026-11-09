package com.nba.simulator.nba_backend_service.controller;

import com.nba.simulator.nba_backend_service.dto.TradeRequestDto;
import com.nba.simulator.nba_backend_service.dto.TradeResponseDto;
import com.nba.simulator.nba_backend_service.service.MlEvaluationService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/trades")
@RequiredArgsConstructor
public class TradeEvaluationController {

    private final MlEvaluationService mlEvaluationService;

    @PostMapping("/evaluate")
    public ResponseEntity<TradeResponseDto> evaluateTrade(@RequestBody TradeRequestDto request) {
        TradeResponseDto evaluation = mlEvaluationService.evaluateTrade(request);
        return ResponseEntity.ok(evaluation);
    }
}