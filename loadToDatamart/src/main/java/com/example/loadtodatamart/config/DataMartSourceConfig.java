package com.example.loadtodatamart.config;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.boot.orm.jpa.EntityManagerFactoryBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;

@Configuration
@EnableTransactionManagement
public class DataMartSourceConfig {

    @Bean(name = "dwDataSource")
    public DataSource dwDataSource() {
        return DataSourceBuilder.create()
                .url("jdbc:mysql://localhost:3306/datawarehouse")
                .username("root")
                .password("")
                .driverClassName("com.mysql.cj.jdbc.Driver")
                .build();
    }

    @Bean(name = "dmDataSource")
    public DataSource dmDataSource() {
        return DataSourceBuilder.create()
                .url("jdbc:mysql://localhost:3306/datamart")
                .username("root")
                .password("")
                .driverClassName("com.mysql.cj.jdbc.Driver")
                .build();
    }

    @Bean(name = "dwJdbcTemplate")
    public JdbcTemplate dwJdbcTemplate(@Qualifier("dwDataSource") DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

    @Bean(name = "dmJdbcTemplate")
    public JdbcTemplate dmJdbcTemplate(@Qualifier("dmDataSource") DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

}
