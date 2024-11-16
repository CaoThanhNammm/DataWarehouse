package org.example.dw21130558_mxt.config;




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

import javax.sql.DataSource;

@Configuration
@EnableTransactionManagement
@EnableJpaRepositories(
        basePackages = "org.example.dw21130558_mxt.repository.control",
        entityManagerFactoryRef = "controlEntityManagerFactory",
        transactionManagerRef = "controlTransactionManager")
public class ControlDataSourceConfig {

    @Bean
    @Primary
    @ConfigurationProperties("app.datasource.control")
    public DataSourceProperties controlDataSourceProperties() {
        return new DataSourceProperties();
    }

    @Bean
    @Primary
    public DataSource controlDataSource() {
        return controlDataSourceProperties().initializeDataSourceBuilder().type(DriverManagerDataSource.class).build();
    }

    @Primary
    @Bean(name = "controlEntityManagerFactory")
    public LocalContainerEntityManagerFactoryBean controlEntityManagerFactory(EntityManagerFactoryBuilder builder) {
        return builder.dataSource(controlDataSource()).packages("org.example.dw21130558_mxt.model.control").build();
    }

    @Primary
    @Bean(name = "controlTransactionManager")
    public PlatformTransactionManager controlTransactionManager(
            final @Qualifier("controlEntityManagerFactory") LocalContainerEntityManagerFactoryBean controlEntityManagerFactory) {
        return new JpaTransactionManager(controlEntityManagerFactory.getObject());
    }

}
