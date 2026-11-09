package com.nba.simulator.nba_backend_service.config;

import com.nba.simulator.nba_backend_service.model.Player;
import com.nba.simulator.nba_backend_service.repository.PlayerRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
@RequiredArgsConstructor
@Slf4j
public class DataInitializer {

    @Bean
    public CommandLineRunner initDatabase(PlayerRepository playerRepository) {
        return args -> {
            if (playerRepository.count() == 0) {
                log.info("Seeding initial NBA player database...");

                List<Player> seedPlayers = List.of(
                    Player.builder()
                        .name("Luka Doncic")
                        .team("DAL")
                        .position("PG")
                        .pts(33.9)
                        .reb(9.2)
                        .ast(9.8)
                        .stl(1.4)
                        .blk(0.5)
                        .tov(4.0)
                        .tsPct(0.617)
                        .usgPct(0.360)
                        .min(37.5)
                        .build(),
                    Player.builder()
                        .name("Mikal Bridges")
                        .team("NYK")
                        .position("SF")
                        .pts(19.6)
                        .reb(4.5)
                        .ast(3.6)
                        .stl(1.0)
                        .blk(0.4)
                        .tov(2.0)
                        .tsPct(0.560)
                        .usgPct(0.245)
                        .min(34.8)
                        .build(),
                    Player.builder()
                        .name("Shai Gilgeous-Alexander")
                        .team("OKC")
                        .position("PG")
                        .pts(30.1)
                        .reb(5.5)
                        .ast(6.2)
                        .stl(2.0)
                        .blk(0.9)
                        .tov(2.2)
                        .tsPct(0.636)
                        .usgPct(0.328)
                        .min(34.4)
                        .build(),
                    Player.builder()
                        .name("Jayson Tatum")
                        .team("BOS")
                        .position("SF")
                        .pts(26.9)
                        .reb(8.1)
                        .ast(4.9)
                        .stl(1.0)
                        .blk(0.6)
                        .tov(2.5)
                        .tsPct(0.607)
                        .usgPct(0.301)
                        .min(35.7)
                        .build()
                );

                playerRepository.saveAll(seedPlayers);
                log.info("Seeded {} NBA players into H2 database.", seedPlayers.size());
            }
        };
    }
}