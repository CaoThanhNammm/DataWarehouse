package com.staging.dh.config;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.autoconfigure.jdbc.DataSourceProperties;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.orm.jpa.EntityManagerFactoryBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;


@Configuration
@EnableTransactionManagement
@EnableJpaRepositories(
		basePackages = "com.staging.dh.repository.staging",
		entityManagerFactoryRef = "stagingEntityManagerFactory",
		transactionManagerRef = "stagingTransactionManager")
public class StagingDataSourceConfig {

	@Bean
	@ConfigurationProperties("app.datasource.staging")
	public DataSourceProperties stagingDataSourceProperties() {
		return new DataSourceProperties();
	}

	@Bean
	public DataSource stagingDataSource() {
		return stagingDataSourceProperties().initializeDataSourceBuilder().type(DriverManagerDataSource.class).build();
	}

	@Bean(name = "stagingEntityManagerFactory")
	public LocalContainerEntityManagerFactoryBean stagingEntityManagerFactory(EntityManagerFactoryBuilder builder) {
		return builder.dataSource(stagingDataSource()).packages("com.staging.dh.model.staging").build();
	}

	@Bean(name = "stagingTransactionManager")
	public PlatformTransactionManager stagingTransactionManager(
			final @Qualifier("stagingEntityManagerFactory") LocalContainerEntityManagerFactoryBean stagingEntityManagerFactory) {
		return new JpaTransactionManager(stagingEntityManagerFactory.getObject());
	}
}