package org.example.dw21130558_mxt.config;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;
@Configuration
@EnableTransactionManagement
public class DatawarehouseSourceConfig {

    @Bean(name = "dwDataSource")
    public DataSource stgDataSource() {
        return DataSourceBuilder.create()
                .url("jdbc:mysql://localhost:3306/staging")
                .username("root")
                .password("")
                .driverClassName("com.mysql.cj.jdbc.Driver")
                .build();
    }

    @Bean(name = "dmDataSource")
    public DataSource dwDataSource() {
        return DataSourceBuilder.create()
                .url("jdbc:mysql://localhost:3306/datawarehouse")
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
