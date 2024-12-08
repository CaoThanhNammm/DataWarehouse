package com.example.loadtodatamart.config;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.autoconfigure.jdbc.DataSourceProperties;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.orm.jpa.EntityManagerFactoryBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;
@Configuration
@EnableTransactionManagement
@EnableJpaRepositories(
		basePackages = "com.example.loadtodatamart.repository.control", // Repository cho database control
		entityManagerFactoryRef = "controlEntityManagerFactory",
		transactionManagerRef = "controlTransactionManager")
public class ControlDataSourceConfig {

	@Primary
	@Bean
	@ConfigurationProperties("app.datasource.control")
	public DataSourceProperties controlDataSourceProperties() {
		return new DataSourceProperties();
	}

	@Primary
	@Bean
	public DataSource controlDataSource() {
		return controlDataSourceProperties()
				.initializeDataSourceBuilder()
				.type(DriverManagerDataSource.class)
				.build();
	}

	@Primary
	@Bean(name = "controlEntityManagerFactory")
	public LocalContainerEntityManagerFactoryBean controlEntityManagerFactory(EntityManagerFactoryBuilder builder) {
		return builder
				.dataSource(controlDataSource())
				.packages("com.example.loadtodatamart.model.control") // Model ánh xạ
				.persistenceUnit("control")
				.build();
	}

	@Primary
	@Bean(name = "controlTransactionManager")
	public PlatformTransactionManager controlTransactionManager(
			@Qualifier("controlEntityManagerFactory") LocalContainerEntityManagerFactoryBean controlEntityManagerFactory) {
		return new JpaTransactionManager(controlEntityManagerFactory.getObject());
	}
}