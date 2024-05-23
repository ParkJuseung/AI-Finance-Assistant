package com.capstone.finance;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
//import org.springframework.boot.autoconfigure.domain.EntityScan;
//import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

//@EnableJpaRepositories(basePackages = {"com.capstone.finance.Repository"}) // com.my.jpa.repository 하위에 있는 jpaRepository를 상속한 repository scan
//@EntityScan(basePackages = {"com.capstone.finance.Entity"})
@SpringBootApplication
public class FinanceApplication {

	public static void main(String[] args) {
		SpringApplication.run(FinanceApplication.class, args);
	}

}
