#include <math.h>
#include <vector>
#include <list>

using namespace std;

double alpha_1 = 1.0; // desvio padrão da velocidade padrão 0.2
double alpha_2 = 0.1; // desvio padrão de theta padrão 0.01
double v_min = 0.0; // velocidade mínima;
double v_max = 25.0; // velocidade máxima

struct particle {};

typedef struct {
    double x;
    double y;
    double theta;
} carmen_point_t, *carmen_point_p;

/*Distribuição normal/gaussiana centrada no valor 'mean'*/
double carmen_gaussian_random(double mean, double std) {
    const double norm = 1.0 / (RAND_MAX + 1.0);
    double u = 1.0 - rand() * norm;                  /* can't let u == 0 */
    double v = rand() * norm;
    double z = sqrt(-2.0 * log(u)) * cos(2.0 * M_PI * v);
    return mean + std * z;
}

/*---------------------------------------------------------------------*/

particle sample_motion_model(double delta_time, particle part_t_1) {

    particle part_t;
    carmen_point_t pose_t;
    carmen_point_t pose_t_1;
    double v;

    /*Copie os dados de 'part_t_1' para 'pose_t_1'*/
    v = part_t_1.velocity;
    pose_t_1.x = part_t_1.pose.x;
    pose_t_1.y = part_t_1.pose.y;
    pose_t_1.theta = part_t_1.pose.theta;

    /*Atualize a velocidade e normalize-a*/
    v = v + carmen_gaussian_random(0.0, alpha_1);
    if (v > v_max) v = v_max;
    if (v < v_min) v = v_min;

    /*Atualize theta e normalize-a*/
    pose_t_1.theta = pose_t_1.theta + carmen_gaussian_random(0.0, alpha_2);
    pose_t_1.theta = carmen_normalize_theta(pose_t_1.theta);

    /*Atualiza a posição da partícula*/
    pose_t.x = pose_t_1.x + delta_time * v * cos(pose_t_1.theta);
    pose_t.y = pose_t_1.y + delta_time * v * sin(pose_t_1.theta);

    /*Preencha os dados da partícula temp*/
    part_t.pose.theta = carmen_normalize_theta(pose_t_1.theta);
    part_t.pose.x = pose_t.x;
    part_t.pose.y = pose_t.y;
    part_t.velocity = v;
    part_t.weight = part_t_1.weight;

    return part_t;
}


/*Retorna a distancia euclidiana entre dois pontos*/
double distance_to_the_nearest_neighbor(double x_z_t, double y_z_t, carmen_point_t pose_t) {
    return 0.0;
}


/*Calcula o peso (valor W) da partciula*/
double calculation_part_weight_pose_reading_model(double dist) {
    return exp(-dist);
}


/*Atualiza o peso e o normaliza para cada partícula*/
void measurement_model(double x, double y, vector<particle> *temp_part_set_t) {

    int num_particles = (int) temp_part_set_t->size();
    auto *distance = (double *) malloc(sizeof(double) * num_particles);
    double sum1 = 0.0;

    int i = 0;

    /*Para cada partícula calcule e armazene a distância entre ela e 'pose'*/
    for (auto it = temp_part_set_t->begin(); it != temp_part_set_t->end(); it++) {
        distance[i] = distance_to_the_nearest_neighbor(x, y, it->pose);
        i++;
    }

    i = 0;

    /*Para cada partícula calcule e armazene seu peso*/
    for (auto it = temp_part_set_t->begin();
         it != temp_part_set_t->end(); it++) {
        it->weight = calculation_part_weight_pose_reading_model(distance[i]);
        sum1 += it->weight;
        i++;
    }

    /*Dado a soma do peso de todas partículas:
     * Para cada partícula normalize-a*/
    for (auto it = temp_part_set_t->begin();
         it != temp_part_set_t->end(); it++) {
        it->weight = (it->weight / sum1);
    }

    free(distance);
}


/* resample particle filter */
void resample(vector<particle> *part_set_t) {
    static double *cumulative_sum = nullptr;
    static particle *temp_particles = nullptr;
    static int num_particles = static_cast<int>(part_set_t->size());

    particle *aux;
    particle *copy_part_set_t = nullptr;
    int i, which_particle;
    double weight_sum;
    double position, step_size;

    /* Allocate memory necessary for resampling */
    cumulative_sum = (double *) calloc(num_particles, sizeof(double));
    carmen_test_alloc(cumulative_sum);
    temp_particles = (particle *) malloc(sizeof(particle) * num_particles);
    carmen_test_alloc(temp_particles);
    copy_part_set_t = (particle *) malloc(sizeof(particle) * num_particles);
    carmen_test_alloc(copy_part_set_t);

    int j = 0;

    /*Preencha as partículas-clones com os dados das existentes*/
    for (auto it = part_set_t->begin(); it != part_set_t->end(); it++) {
        copy_part_set_t[j].pose.x = it->pose.x;
        copy_part_set_t[j].pose.y = it->pose.y;
        copy_part_set_t[j].pose.theta = it->pose.theta;
        copy_part_set_t[j].velocity = it->velocity;
        copy_part_set_t[j].weight = it->weight;
        j++;
    }

    weight_sum = 0.0;

    /*Some o peso de todas partículas-clones*/
    for (i = 0; i < num_particles; i++) {

        /* Sum the weights of all of the particles */
        weight_sum += copy_part_set_t[i].weight;
        cumulative_sum[i] = weight_sum;
    }

    /* choose random starting position for low-variance walk */
    position = carmen_uniform_random(0, weight_sum);
    step_size = weight_sum / (double) num_particles;
    which_particle = 0;

    /* draw num_particles random samples */
    for (i = 0; i < num_particles; i++) {
        position += step_size;

        if (position > weight_sum) {
            position -= weight_sum;
            which_particle = 0;
        }

        while (position > cumulative_sum[which_particle])
            which_particle++;

        temp_particles[i] = copy_part_set_t[which_particle];
    }

    /* Switch particle pointers */
    aux = copy_part_set_t;
    copy_part_set_t = temp_particles;
    temp_particles = aux;

    int m = 0;
    for (auto it = part_set_t->begin(); it != part_set_t->end(); it++) {
        it->pose.x = copy_part_set_t[m].pose.x;
        it->pose.y = copy_part_set_t[m].pose.y;
        it->pose.theta = copy_part_set_t[m].pose.theta;
        it->velocity = copy_part_set_t[m].velocity;
        it->weight = copy_part_set_t[m].weight;
        m++;
    }

    free(temp_particles);
    free(cumulative_sum);
    free(copy_part_set_t);
}

double calculate_degeneration_of_the_particles(vector<particle> *part_set_t) {
    double effective_sample_size;
    double sum_of_squared_weights = 0.0;

    for (auto it = part_set_t->begin();
         it != part_set_t->end(); it++) {
        sum_of_squared_weights += it->weight * it->weight;
    }

    effective_sample_size = 1 / sum_of_squared_weights;

    return effective_sample_size;
}

vector<particle> algorithm_monte_carlo(
        vector<particle> *part_set_t_1, double x, double y,
        double delta_time, pcl::PointCloud <pcl::PointXYZ> pcl_cloud) {

    vector<particle> temp_part_set_t;
    vector<particle> part_set_t;

    /*Predição*/
    for (auto it = part_set_t_1->begin(); it != part_set_t_1->end(); it++) {
        particle part_t;
        particle part_t_1;
        part_t_1.pose.x = it->pose.x;
        part_t_1.pose.y = it->pose.y;
        part_t_1.pose.theta = it->pose.theta;
        part_t_1.velocity = it->velocity;
        part_t_1.weight = it->weight;

        part_t = sample_motion_model(delta_time, part_t_1);
        temp_part_set_t.push_back(part_t);
    }

    /*Mensuração*/
    measurement_model(x, y, &temp_part_set_t);

    /*Sorteamento de amostragem (RESAMPLING)*/
    resample(&temp_part_set_t);

    part_set_t = temp_part_set_t;

    return part_set_t;
}