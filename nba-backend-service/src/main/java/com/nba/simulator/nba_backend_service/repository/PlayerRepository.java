package com.nba.simulator.nba_backend_service.repository;

import com.nba.simulator.nba_backend_service.model.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PlayerRepository extends JpaRepository<Player, Long> {
    Optional<Player> findByNameIgnoreCase(String name);
}